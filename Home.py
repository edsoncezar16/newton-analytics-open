import streamlit as st


st.title("Projeto Newton Analytics")


st.markdown(
    """
    As análises apresentadas aqui têm por objetivo utilizar os dados das atividades do 
    Projeto Newton nos últimos semestres para entender, quantitativamente, qual o real
    impacto das atividades do projeto no desempenho dos estudantes.


Em resumo, os direcionamentos que esta análises buscaram responder foram os seguintes:


## Distribuição da turma relativa à participação nas avaliações principais:
- Quantos discentes estavam matriculados no período? Chamemos este número de M.

Quantidades e percentuais (relativos a M) de discentes que:
    
- Grupo A) Realizaram apenas uma prova no período? Em 2023-2, trocar para "de uma a quatro".
- Grupo B) Realizaram apenas duas provas no período? Em 2023-2, trocar para "de cinco a oito".
- Grupo C) Realizaram as três provas no período? Em 2023-2, trocar para "de nove a doze".
- Grupo D) Foram aprovados no período (isto é, tiveram média final maior ou igual a cinco).


## Distribuição e desempenho da turma relativos às atividades da monitoria:

- Listas de Exercícios: considerar a quantidade L de listas por cada discente no período. (2022-2, 2022-4, 2023-2)

- Plantões: considerar a quantidade de vezes P que cada discente foi ao plantão. (2022-4)

- Sessões de Monitoria das sextas-feiras: considerar a quantidade de vezes S que cada discente foi nas sextas-feiras, e a frequência S_rel de cada discente relativa ao número de sessões realizadas no período. (2022-4)

- Oficinas: considerar a quantidade O de vezes que cada discente foi a oficinas, e a frequência
O_rel de cada discente relativa ao número de oficinas realizadas no período. (2022-4, 2023-2)

## Perguntas Principais

- Quantos discentes tem L, P, S e O exatamente iguais a cada um dos valores possíveis?

- Quais os percentuais relativos a M, A, B, C e D de discentes que têm L, P, S e O iguais a cada um dos valores possíveis?

- Para cada um dos valores possíveis de L, P, S e O, qual foi a média das médias finais?

- Para cada um dos valores possíveis de L, P, S e O, qual foi o percentual médio de aprovação?

"""
)
