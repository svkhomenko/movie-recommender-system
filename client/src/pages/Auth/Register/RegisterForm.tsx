import { useForm } from 'react-hook-form';
import { Input, Button, VStack, Field } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema } from '~/validation/auth';
import type { IRegister } from '~/validation/auth';
import { useRegisterMutation } from '~/store/api/authSlice';
import { useNavigate } from 'react-router-dom';
import useRequestHandler from '~/hooks/useRequestHandler';
import styles from '../auth.styles';

const RegisterForm = () => {
  const [registerMutation, { isLoading }] = useRegisterMutation();
  const navigate = useNavigate();

  const { handler: registerHandler } = useRequestHandler<IRegister>({
    f: registerMutation,
    successMsg: 'You are successfully registered. Please check your email to confirm it',
    successF: () => {
      navigate('/login');
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<IRegister>({
    resolver: zodResolver(registerSchema),
  });

  return (
    <form onSubmit={handleSubmit(registerHandler)}>
      <VStack gap="4">
        <Field.Root invalid={!!errors.email} required>
          <Field.Label htmlFor="email">Email</Field.Label>
          <Input id="email" placeholder="email" {...register('email')} />
          <Field.ErrorText>{errors.email?.message}</Field.ErrorText>
        </Field.Root>

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

        <Button type="submit" css={styles.button} loading={isLoading} spinnerPlacement="end" loadingText="Submitting">
          Sign up
        </Button>
      </VStack>
    </form>
  );
};

export default RegisterForm;
