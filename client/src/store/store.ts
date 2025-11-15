import { configureStore, combineReducers } from '@reduxjs/toolkit';
import profileReducer from './profileSlice';
import { apiSlice } from './api/apiSlice';
import { tmdbApiSlice } from './tmdbApi/tmdbApiSlice';
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from 'redux-persist';

const persistConfig = {
  key: 'root',
  storage,
  blacklist: [apiSlice.reducerPath, tmdbApiSlice.reducerPath],
};

const persistedReducer = persistReducer(
  persistConfig,
  combineReducers({
    profile: profileReducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
    [tmdbApiSlice.reducerPath]: tmdbApiSlice.reducer,
  }),
);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware: any) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(apiSlice.middleware)
      .concat(tmdbApiSlice.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export const persistor = persistStore(store);
