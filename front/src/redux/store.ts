import { configureStore } from '@reduxjs/toolkit'
import globalContextReducer from './globalContextSlice'

export const store = configureStore({
  reducer: {
    globalContext: globalContextReducer
  },
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch