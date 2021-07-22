# Discord.py Music Bot

Um bot de música simples escrito em discord.py usando youtube-dl. Use isso como um exemplo ou uma base para seu próprio bot e estenda-o como quiser.

### Pre-Setup

Se você ainda não tem um discord bot, clique [aqui] (https://discordapp.com/developers/), aceite as solicitações e clique em "Novo aplicativo" no canto superior direito da tela. Digite o nome do seu bot e clique em aceitar. Clique no bot no painel da esquerda e clique em "Adicionar bot". Quando o prompt aparecer, clique em "Sim, faça!"
![Left panel](https://i.imgur.com/hECJYWK.png)

Em seguida, clique em copiar sob o token para obter o token do seu bot. O ícone do seu bot também pode ser alterado enviando uma imagem.

![Bot token area](https://i.imgur.com/da0ktMC.png)

### Setup

Criar arquivo `.env`

Adicionar `TOKEN=<your bot token>`

Seu arquivo .env deve ser parecido com este:

```
TOKEN=<Bot token>
```

### Uptime

Para manter seu bot vivo, você precisa transformar esta repl em um servidor web. A maneira como você faz isso é que você `import keep_alive`e execute depois `keep_alive()`.

Agora que este repl é um servidor, tudo que você precisa fazer para manter seu bot ativo é configurar algo para executar o ping no site que seu bot fez a cada 5 minutos ou mais.

Depois entre no [uptimerobot.com](https://uptimerobot.com/) e crie uma conta se você não tiver uma.  Após verificar sua conta, clique em "Adicionar Novo Monitor".

+ Para Tipo de monitor, selecione "HTTP (s)"
+ Em Nome Amigável coloque o nome do seu bot
+ Para o seu url, coloque o url do site feito para o seu repl.
+ Selecione os contatos de alerta desejados e clique em "Criar Monitor"
![Uptime robot example](https://i.imgur.com/Qd9LXEy.png)

Seu bot agora deve estar pronto para funcionar, com quase 100% de tempo de atividade.

