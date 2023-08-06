# b2-utils

## Passos
- Em caso de ser sua primeira vez publicando a lib no pipy é necessario um arquivo de configuração no home do computador com o nome .pypirc para mais informações confira o forum no click up sobre como preencher o arquivo.
- Antes de rodar o script para publicar a lib no pip é necessario subir a versão dela no pyproject.toml.

```toml
[project]
name = "b2-utils"
version = "0.X.XX"
```

- Logo apos é necessario o rodar o script que compila as dependencias ./compile.sh
- Por fim só publicar ser feliz.
