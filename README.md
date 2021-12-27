# webmotors-crawler

Fiz esse crawler pra pesquisar carros na Webmotors de maneira mais analítica. Para usá-lo:

1 - Vá até a Webmotors, aperte F12 para abrir a janela inspecionar. Selecione a aba Network e ative o filtro Fetch/XHR
2 - Faça uma pesquisa que desejar (valor, preço, cidade). Quando isso acontecer, haverá movimentação nessa aba. Procure a chamada que começa com "car?"
3 - Nesta chamada, vá até a aba Headers, e copie o Request Url até o final do "actualPage="
4 - Cole este endereço na linha 32 como variável Url. Tome cuidado para não apagar o final dela, onde a paginação variável vai