interface IContext {
  context: string
}

type ArticleState = {
  payload: IContext[]
}

type ArticleAction = {
  type: string
  payload: IContext
}

type DispatchType = (args: ArticleAction) => ArticleAction