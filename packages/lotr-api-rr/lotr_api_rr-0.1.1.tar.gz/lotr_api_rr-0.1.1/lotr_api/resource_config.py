from dataclasses import dataclass

from lotr_api.schemas import SchemaType


# API operation type
class OperationType:
    GET_ONE = 'get_one'
    GET_MANY = 'get_many'


# Helper class to define resource configuration
@dataclass
class ResourceConfig:
    name: str
    endpoint: str
    schema: SchemaType
    supported_operations: list[OperationType]
    sub_resources: list

    def get_operations(self):
        operations = []
        for op in self.supported_operations:
            if op == OperationType.GET_ONE:
                operations.append(f'{self.name}_get')
            if op == OperationType.GET_MANY:
                operations.append(f'{self.name}_list')
        return operations
