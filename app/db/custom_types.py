from sqlalchemy import Numeric

EvmUint256 = Numeric(precision=len(str(2**256)), scale=18)
