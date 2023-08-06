from typing import Dict, Any
from rds.core.transformers.fields import Field


class EstabelecimentoCodigoUnidadeField(Field):
    def __init__(self, codigo_municipio_fieldname: str, cnes_fieldname: str):
        super().__init__(None)
        self.cnes_fieldname = cnes_fieldname
        self.codigo_municipio_fieldname = codigo_municipio_fieldname

    def transform_to_dict(
        self,
        source_dict: Dict[str, Any],
        destination_dict: Dict[str, Any],
        destination_fieldname: str,
    ):
        destination_dict[destination_fieldname] = (
            source_dict[self.codigo_municipio_fieldname] + source_dict[self.cnes_fieldname]
        )
