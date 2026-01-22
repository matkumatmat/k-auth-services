from dataclasses import dataclass

@dataclass
class ServerConfig:
    environtment: str
    # debug: bool

    def is_production(self) -> bool:
        return self.environtment == "production"