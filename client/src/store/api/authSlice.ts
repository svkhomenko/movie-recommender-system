import { logout, setUserAndToken } from '../profileSlice';
import { apiSlice } from './apiSlice';
import type { IRegister } from '~/validation/auth';
import type { IUser, IAccessToken } from '~/types/user';

export const extendedApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    register: builder.mutation<void, IRegister>({
      query: ({ passwordConfirm, ...body }) => ({
        url: 'auth/register',
        method: 'POST',
        body: body,
      }),
    }),
    login: builder.mutation<IUser & { accessToken: IAccessToken }, FormData>({
      query: (body) => ({
        url: 'auth/login',
        method: 'POST',
        body: body,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }),
      async onQueryStarted(_args, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(setUserAndToken(data));
        } catch (error) {}
      },
      invalidatesTags: ['UserProfile'],
    }),
    logout: builder.mutation<void, void>({
      query: () => ({
        url: 'auth/logout',
        method: 'POST',
      }),
      async onQueryStarted(_args, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          dispatch(logout());
        } catch (error) {}
      },
    }),
    confirmEmail: builder.mutation<void, { confirmToken: string }>({
      query: ({ confirmToken }) => ({
        url: `auth/confirm-email/${confirmToken}`,
        method: 'POST',
      }),
    }),
    sendPasswordConfirmation: builder.mutation({
      query: ({ email }) => ({
        url: 'auth/password-reset',
        method: 'POST',
        body: { email },
      }),
    }),
    resetPassword: builder.mutation({
      query: ({ confirmToken, password }) => ({
        url: `auth/password-reset/${confirmToken}`,
        method: 'POST',
        body: { password },
      }),
    }),
  }),
});

export const {
  useRegisterMutation,
  useLoginMutation,
  useLogoutMutation,
  useConfirmEmailMutation,
  useSendPasswordConfirmationMutation,
  useResetPasswordMutation,
} = extendedApiSlice;
