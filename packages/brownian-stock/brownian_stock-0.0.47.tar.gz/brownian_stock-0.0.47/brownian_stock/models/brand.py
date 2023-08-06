from typing import Any


class Brand:

    """銘柄情報を扱うクラス"""

    def __init__(
        self,
        code: str,
        company_name: str,
        sector17: str,
        sector33: str,
        scale_category: str,
        market_code: str,
        company_name_english: str,
        margin_code: str,
    ) -> None:
        self.code = code
        self.company_name = company_name
        self.company_name_english = company_name_english
        self._sector17 = sector17
        self._sector33 = sector33
        self.scale_category = scale_category
        self.market_code = market_code
        self.margin_code = margin_code

    @property
    def sector17(self) -> str:
        return self._sector17

    @property
    def sector33(self) -> str:
        return self._sector33

    def __repr__(self) -> str:
        return self.company_name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Brand):
            raise TypeError("other must be Brand object.")
        return other.code == self.code
