# IgnitorRF

Este projeto contém um script Python assíncrono para controle de ignitores de foguetes via Rádio Frequência.

## Requisitos

- Python 3.7+
- Bibliotecas:
    - `customtkinter`
    - `pyserial`

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/ViniciusCMB/IgnitorRF.git
cd IgnitorRF
pip install -r requirements.txt
```

## Uso

Execute o script `async_ign.py` para iniciar o controle dos ignitores usando uma interface gráfica:

```bash
python async_ign.py
```
Ou execute o script `async_cmd.py` para iniciar o controle dos ignitores usando linha de comando:

```bash
python async_ign.py
```

## Estrutura do Projeto

- `async_ign.py`: Script para controle assíncrono dos ignitores via RF usando user interface.
- `async_cmd.py`: Script para controle assíncrono dos ignitores via RF usando command line.
- `README.md`: Documentação do projeto.

## Features



## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.
