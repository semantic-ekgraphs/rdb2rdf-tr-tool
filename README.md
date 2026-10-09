# rdb2rdf-tr-tool
RDB2RDF Transformation Rules Tool

---
# Running the Back-end

`fatsapi dev`


Analise os dois arquivos anexos com cuidado. 
Junte as ideias dos dois documentos.
Organize as ideias e elabore um framework resultante dessa junção. 
Use apenas os textos explícitos nos dois documentos.
Não invente, crie, proponha ou sugira, use apenas os textos dos anexos.
Se necessário, corrija sintátice e semânticamente a escrita.
A saída deve ser em PDF.


Stage 2

Agent suggested by Gemini:
Principais pontos garantidos nesta definição:Sem Ambiguidade (Cobertura Completa das Subetapas): Incorpora claramente tanto a subetapa 2.1 (Trigger Planning) quanto a 2.2 (Trigger Synthesis and Static Verification) descritas no texto.Especificidade Teórica: Cita explicitamente o cálculo de $Relev(R)$, a distinção entre regras pivot-relevant e relation-relevant, e a geração de todas as estruturas algébricas de changeset ($A^-$, $A^+$, $S2$, $\Delta^+_{pivot}$, $\Delta^+_{rel}$ e $\Delta^+$).Restrições Técnicas do PostgreSQL: Reforça o uso obrigatório de gatilhos pós-operação em nível de instrução (statement-level AFTER triggers) acoplados às tabelas de transição para popular a fila de manutenção assíncrona (asynchronous maintenance queue).