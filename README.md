Este projeto foi desenvolvido como parte da disciplina de Arquitetura de Computadores e tem como objetivo a criação de um simulador de Falha de Proteção Geral (GPF – General Protection Fault). O simulador busca representar, de forma didática e interativa, o comportamento da arquitetura x86 em modo real quando ocorrem acessos inválidos entre diferentes segmentos de memória, como CS, DS, SS e ES.

A ferramenta permite ao usuário inserir valores manuais nos registradores de segmento e offset, calcular os endereços físicos e verificar, com base em regras definidas, se há invasão de espaço entre segmentos que configure uma falha de proteção. O sistema também apresenta uma visualização gráfica da memória segmentada, destacando os limites de cada segmento e evidenciando visualmente os conflitos que causam a GPF.

Além de contribuir para a compreensão dos conceitos de segmentação de memória e proteção entre segmentos, o simulador é útil como recurso didático para análise prática dos mecanismos de proteção presentes nas arquiteturas de processadores.

grupo responsavel:

Gabriel Barreto:
- interface com tkinter

Daniel Barreto:
- def responsavel por calcular os intervalos de cada segmento
- def responsavel opor identificar

Davi JC:
- def responsavel por verificar se ocorre a gpf dentro do simulador

Lucas Soares:
- def de calcular o end fisico
- def para idenfificar em qual segmento o endereço vai cair


Observação: Outras funcionalidades que não foram listadas provavelmente foram desenvolvidas em conjunto com as demais, fazendo parte da construção integrada do projeto.
 
