import { useForm } from 'react-hook-form';
import { Input, Button, VStack, Field } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { resetPasswordSchema } from '~/validation/auth';
import type { IResetPassword } from '~/validation/auth';
import { useResetPasswordMutation } from '~/store/api/authSlice';
import { useSearchParams } from 'react-router-dom';
import { useAppSelector } from '~/hooks/useAppSelector';
import { customToaster } from '~/components/ui/toaster';
import styles from '../auth.styles';

const PasswordReset = () => {
  const [resetPassword, { isLoading }] = useResetPasswordMutation();
  let [searchParams] = useSearchParams();
  const confirmToken = searchParams.get('token') || useAppSelector((state) => state.profile).accessToken;

  const onSubmit = async (data: IResetPassword) => {
    try {
      await resetPassword({ ...data, confirmToken }).unwrap();
      customToaster({
        description: 'Password was successfully updated',
        type: 'success',
      });
      reset();
    } catch (error: any) {
      customToaster({
        description: error.data.message,
        type: 'error',
      });
    }
  };

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<IResetPassword>({
    resolver: zodResolver(resetPasswordSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <VStack gap="4">
        <Field.Root invalid={!!errors.password}>
          <Field.Label htmlFor="password">Password</Field.Label>
          <Input id="password" placeholder="password" type="password" {...register('password')} />
          <Field.ErrorText>{errors.password?.message}</Field.ErrorText>
        </Field.Root>

        <Field.Root invalid={!!errors.passwordConfirm}>
          <Field.Label htmlFor="passwordConfirm">Password confirmation</Field.Label>
          <Input
            id="passwordConfirm"
            placeholder="password confirmation"
            type="password"
            {...register('passwordConfirm')}
          />
          <Field.ErrorText>{errors.passwordConfirm?.message}</Field.ErrorText>
        </Field.Root>

        <Button type="submit" css={styles.button} loading={isLoading} loadingText="Submitting">
          Reset password
        </Button>
      </VStack>
    </form>
  );
};

export default PasswordReset;
