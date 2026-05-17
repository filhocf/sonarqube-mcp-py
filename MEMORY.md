# MEMORY.md — sonarqube-mcp-py

## Estado Atual

- **Versão**: 0.1.0
- **PyPI**: https://pypi.org/project/sonarqube-mcp-py/
- **Transporte**: stdio (default) ou streamable-http (porta 8959)
- **SonarQube**: https://qa.prevnet (Dataprev, requer VPN)
- **Lazy**: não conecta no startup, só quando tool é chamada

## Contexto

- Substitui o JAR Java oficial (SonarSource/sonarqube-mcp-server)
- Python puro, sem dependência de JVM
- 13 tools, 12 testes
