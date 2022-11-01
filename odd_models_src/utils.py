import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Parenthesis, T, TokenList
from sqlparse.tokens import Punctuation


def _is_in_table(token):
    return _match_on(
        token,
        [
            "FROM",
            "INNER JOIN",
            "JOIN",
            "FULL JOIN",
            "FULL OUTER JOIN",
            "LEFT JOIN",
            "LEFT OUTER JOIN",
            "RIGHT JOIN",
            "RIGHT OUTER JOIN",
        ],
    )


def _is_out_table(token):
    return _match_on(token, ["INTO", "TO"])


def _match_on(token, keywords):
    return token.match(T.Keyword, values=keywords)


class SqlParser:
    def __init__(self, sql):
        self._sql = sql
        self._inputs = set()
        self._outputs = set()
        self._idx = None
        self.ctes = set()

    def _get_tables(self, tokens):
        def parse_ident(ident: Identifier) -> str:
            token_list = ident.flatten()
            table_name = next(token_list).value
            try:
                dot = next(token_list)
                if dot.match(Punctuation, "."):
                    table_name += dot.value
                    table_name += next(token_list).value
                else:
                    table_name = f"{table_name}"
            except StopIteration:
                table_name = f"{table_name}"
            return table_name

        self._idx, token = tokens.token_next(idx=self._idx)
        tables = []
        if isinstance(token, IdentifierList):
            gidx = 0
            tables.append(parse_ident(token.token_first(skip_ws=True, skip_cm=True)))
            gidx, punc = token.token_next(gidx, skip_ws=True, skip_cm=True)
            while punc and punc.value == ",":
                gidx, name = token.token_next(gidx, skip_ws=True, skip_cm=True)
                tables.append(parse_ident(name))
                gidx, punc = token.token_next(gidx)
        else:
            tables.append(parse_ident(token))

        return tables

    def is_cte(self, token: T):
        return token.match(T.Keyword.CTE, values=["WITH"])

    def get_response(self):
        self.get_tokens()
        return self.get_inputs(), self.get_outputs()

    def get_tokens(self):
        stats = sqlparse.parse(self._sql)
        tokens = TokenList(stats[0].tokens)
        self._idx, token = tokens.token_next_by(t=T.Keyword)
        while token:
            if self.is_cte(token):
                cte_name, cte_intables = self.parse_cte(tokens)
                for intable in cte_intables:
                    if intable not in self.ctes:
                        self._inputs.add(intable)
            elif _is_in_table(token):
                extracted_tables = self._get_tables(tokens)
                for table in extracted_tables:
                    if table not in self.ctes:
                        self._inputs.add(table)
            elif _is_out_table(token):
                extracted_tables = self._get_tables(tokens)
                self._outputs.add(extracted_tables[0])
            self._idx, token = tokens.token_next_by(t=T.Keyword, idx=self._idx)

    def parse_cte(self, tokens: TokenList):
        gidx, group = tokens.token_next(self._idx, skip_ws=True, skip_cm=True)

        # handle recursive keyword
        if group.match(T.Keyword, values=["RECURSIVE"]):
            gidx, group = tokens.token_next(gidx, skip_ws=True, skip_cm=True)

        if not group.is_group:
            return [], None

        # get CTE name
        offset = 1
        cte_name = group.token_first(skip_ws=True, skip_cm=True)
        self.ctes.add(cte_name.value)

        # AS keyword
        offset, as_keyword = group.token_next(offset, skip_ws=True, skip_cm=True)
        if not as_keyword.match(T.Keyword, values=["AS"]):
            raise RuntimeError(f"CTE does not have AS keyword at index {gidx}")

        offset, parens = group.token_next(offset, skip_ws=True, skip_cm=True)
        if isinstance(parens, Parenthesis) or parens.is_group:
            # Parse CTE using recursion.
            return cte_name.value, self.recurse(TokenList(parens.tokens)).in_tables
        raise RuntimeError(f"Parens {parens} are not Parenthesis at index {gidx}")

    def get_inputs(self):
        return list(self._inputs)

    def get_outputs(self):
        return list(self._outputs)
