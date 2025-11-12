import { useForm } from 'react-hook-form';
import { Input, Button, VStack, Field } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema } from '~/validation/auth';
import type { ILogin } from '~/validation/auth';
import { useLoginMutation } from '~/store/api/authSlice';
import { useNavigate } from 'react-router-dom';
import useRequestHandler from '~/hooks/useRequestHandler';
import styles from '../auth.styles';

const LoginForm = () => {
  const [login, { isLoading }] = useLoginMutation();
  const navigate = useNavigate();

  const { handler: loginHandler } = useRequestHandler<FormData>({
    f: login,
    successF: () => {
      navigate('/');
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ILogin>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = handleSubmit(async ({ username, password }) => {
    const form = new FormData();
    form.append('username', username);
    form.append('password', password);
    await loginHandler(form);
  });

  return (
    <form onSubmit={onSubmit}>
      <VStack gap="5">
        <Field.Root invalid={!!errors.username} required>
          <Field.Label htmlFor="username">Email</Field.Label>
          <Input id="username" placeholder="email" {...register('username')} />
          <Field.ErrorText>{errors.username?.message}</Field.ErrorText>
        </Field.Root>
        <Field.Root invalid={!!errors.password}>
          <Field.Label htmlFor="password">Password</Field.Label>
          <Input id="password" placeholder="password" type="password" {...register('password')} />
          <Field.ErrorText>{errors.password?.message}</Field.ErrorText>
        </Field.Root>
        <Button type="submit" css={styles.button} loading={isLoading} spinnerPlacement="end" loadingText="Submitting">
          Log in
        </Button>
      </VStack>
    </form>
  );
};

export default LoginForm;
