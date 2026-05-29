export const languages = {
  global: {
    resource: (lang: string) => lang == "pt"
      ? "Recurso"
      : "Resource"
  },
  repository: {
    title: (lang: string) => lang == "pt"
      ? "Seleção de Repositório"
      : "Repostory Selection"
  },
  extract_schema: {
    title: (lang: string) => lang == "pt"
      ? "Seleção de Esquema"
      : "Schema Selection"
  },
  home: {
    caption: (lang: string) => lang == "pt"
      ? "Uma Ferramenta para Construção e Exploração Contextual da Visão Semântica em Sistemas de EKG."
      : "A Tool for Contextual Construction and Exploration of Semantic View in Enterprise Knowledge Graph Systems"
  }
}

