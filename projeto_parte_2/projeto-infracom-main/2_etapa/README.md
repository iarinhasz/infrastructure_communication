# Primeira etapa: Envio de arquivos via UDP

## Inicializando o código

Inicialize o cliente

    python ./cliente.py

Em outra janela, inicialize o servidor

    python ./servidor.py

## Simulando perda de pacotes

Perdas de pacotes podem ser simuladas alterando a variável `SEND_PROBABILITY` em `sender.py` e `receiver.py`, de acordo com qual lado se deseja simular a perda. Esta variável define a probabilidade que um pacote seja enviado com sucesso por uma máquina.

Logo com `SEND_PROBABILITY = 1`, os pacotes sempre irão ser enviados. Com `SEND_PROBABILITY = 0.5`, os pacotes serão enviados apenas 50% das vezes.

```python
# ./sender.py

class Sender:
    SEND_PROBABILITY = 0.8 # ocasiona 20% de perdas
```

O funcionamento desta simulação é definida em `common.py`:

```python
# ./common.py

# Envia pacotes via UDP. simula perdas de acordo com probability
def udt_send(...probability=1.0):
    ...
    if rand < probability:
        return self.sock.sendto(data, address)
    else:
        printc("== ! Simulando falha na transmissão ! ==", bcolors.FAIL)
        return 0
    ...
```

## Funcionamento

O cliente possui uma interface de comandos para facilitar a interação

### Detalhes sobre pacotes

Todo pacote enviado tanto pelo cliente quanto pelo servidor terá adicionado um header, indicando uma sequencia de caracteres que identifique o pacote `"HELLOPKT"`, os numeros `seq` e `ack`, e o conteudo do pacote

### Envio de strings

Apenas digite qualquer coisa na linha de comando do cliente para enviar uma string para o servidor

### Envio de arquivos

1. Digite `arquivo` ou `arq` para enviar um arquivo ao servidor
2. Insira o caminho do arquivo relativo à pasta em que foi executado o comando de compilar o cliente
   1. Por exemplo, para enviar um dos arquivos de teste, digite `../test_files/cheems.png`
   2. Ou, para enviar o próprio código do cliente, `./cliente.py`
3. O arquivo será enviado ao servidor junto com um *header* que irá conter as seguintes informações
   1. Uma mensagem especificando o inicio do header
   2. O nome do arquivo e sua extensão
   3. O tamanho, em *bytes* do arquivo
   4. *(opcional)* Uma mensagem extra, se for necessário debugar algo
4. O arquivo será enviado em pacotes de tamanho `buffer_size`, definido em `common.py` como `1024 bytes`
5. O servidor irá receber, primeiramente, o *header*, que lhe informará a quantidade de bytes que ele estará esperando receber
6. A medida que o servidor recebe pacotes do cliente, ele irá os salvando em um arquivo com a mesma extensão
7. Quando a transferência é completada, o arquivo é enviado de volta ao cliente, repetindo as etapas a partir do passo 3
8. Os arquivos do recebidos no cliente e servidor podem ser encontrados em `files_client/` e `files_server/` (ou nos caminhos especificados em `CLIENT_DIR` e `SERVER_DIR`)

### Nome dos arquivos

Para explicitar o funcionamento do código, o arquivo, quando recebido pelo servidor, terá o codigo `s_` adicionado ao inicio do nome descrito no header.

   1. Quando este é recebido pelo cliente, ele terá o código `c_` adicionado ao inicio do nome descrito no header.
   2. Desta forma, sendo o arquivo original `nome.txt`, o servidor irá o salvar (e enviar ao cliente) como `s_nome.txt`, e o cliente irá o salvar como `c_s_nome.txt`

### Timeout

Seguindo o que é definido no RDT 3.0, o `Sender` irá iniciar um temporizador (duração padrão de 2 segundos) toda vez que um pacote for transmitido. Caso o temporizador estoure, ele será retransmitido

```python
# ./sender.py

# alterar delay padrão do temporizador
def start_timer(self, duration=2):
```

### Modificando o endereço do servidor/cliente

O cliente e servidor, por padrão, estão ambos localizados em `localhost`, nas portas `1337` e `5000`, respectivamente. Para alterar o endereço de um deles, basta modificar o código que chama o inicializador da classe de utilidades `Socket`:

```python
# ./cliente.py

# inicializar cliente na porta 1337, IP padrão (localhost)
client = Socket(port=1337)
...
```

```python
# ./servidor.py

# inicializar servidor na porta 2000, IP localhost
server = Socket(ip="localhost", port=2000)
...
```

Para alterar o destino de envio dos arquivos, basta modificar as seguintes variaveis em `cliente.py`:

```python
# ./cliente.py

...
# definir servidor para onde vao ser enviados os arquivos
server_ip = "localhost"
server_port = 5000
...
```

### Envio entre máquinas diferentes

Para testar o envio entre máquinas diferentes, certifique-se de definir o IP do servidor como `0.0.0.0`

```python
# ./servidor.py

# inicializar servidor na porta 2000, IP 0.0.0.0
server = Socket(ip="0.0.0.0", port=2000)
...
```
