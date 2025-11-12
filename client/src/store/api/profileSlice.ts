import { apiSlice } from './apiSlice';
import { logout, updateUser } from '../profileSlice';
import type { IUpdate } from '~/validation/profile';

type IResUpdate = { is_active: boolean };

export const profileSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    updateProfile: builder.mutation<IResUpdate, IUpdate>({
      query: (body) => ({
        url: 'profile',
        method: 'PUT',
        body: body,
      }),
      async onQueryStarted(body, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          if (data.is_active) {
            dispatch(updateUser(body));
          } else {
            dispatch(logout());
          }
        } catch (error) {}
      },
      invalidatesTags: ['UserProfile'],
    }),
    deleteProfile: builder.mutation({
      query: () => ({
        url: 'profile',
        method: 'DELETE',
      }),
      async onQueryStarted(_args, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          dispatch(logout());
        } catch (error) {}
      },
      invalidatesTags: ['UserProfile'],
    }),
  }),
});

export const { useUpdateProfileMutation, useDeleteProfileMutation } = profileSlice;
