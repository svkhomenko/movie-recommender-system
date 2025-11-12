import { useForm } from 'react-hook-form';
import { Input, Button, VStack, Field } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { sendPasswordConfirmationSchema, type ISendPasswordConfirmation } from '~/validation/auth';
import { useSendPasswordConfirmationMutation } from '~/store/api/authSlice';
import { customToaster } from '~/components/ui/toaster';
import styles from '../auth.styles';

const SendPasswordConfirmationForm = () => {
  const [sendPasswordConfirmation, { isLoading }] = useSendPasswordConfirmationMutation();

  const onSubmit = async (data: ISendPasswordConfirmation) => {
    try {
      await sendPasswordConfirmation(data).unwrap();
      customToaster({
        description: `Password reset confirmation sent to email ${data.email}`,
        type: 'success',
      });
      reset();
    } catch (error: any) {
      customToaster({
        description: error.data.detail,
        type: 'error',
      });
    }
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ISendPasswordConfirmation>({
    resolver: zodResolver(sendPasswordConfirmationSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <VStack gap="4">
        <Field.Root invalid={!!errors.email} required>
          <Field.Label htmlFor="email">Email</Field.Label>
          <Input id="email" placeholder="email" {...register('email')} />
          <Field.ErrorText>{errors.email?.message}</Field.ErrorText>
        </Field.Root>

        <Button type="submit" css={styles.button} loading={isLoading} loadingText="Submitting">
          Request password reset
        </Button>
      </VStack>
    </form>
  );
};

export default SendPasswordConfirmationForm;
