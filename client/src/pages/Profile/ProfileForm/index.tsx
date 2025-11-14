import { Button, Card, Heading, Input, VStack, Field } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useAppSelector } from '~/hooks/useAppSelector';
import { useUpdateProfileMutation } from '~/store/api/profileSlice';
import { customToaster } from '~/components/ui/toaster';
import { updateSchema, type IUpdate } from '~/validation/profile';
import styles from '../profile-card.styles';

type IProps = { setIsEdit: React.Dispatch<React.SetStateAction<boolean>> };

const ProfileForm = ({ setIsEdit }: IProps) => {
  const { user } = useAppSelector((state) => state.profile);

  const [update, { isLoading }] = useUpdateProfileMutation();
  const { id, role, ...defaultValues } = user;

  const updateHandler = async (data: IUpdate) => {
    try {
      const { is_active } = await update(data).unwrap();
      if (is_active) {
        customToaster({
          description: "You've successfully updated your profile",
          type: 'success',
        });
      } else {
        customToaster({
          description:
            "You've successfully updated your profile. Please confirm your email. A corresponding letter has been sent to the provided email address",
          type: 'success',
        });
      }
      setIsEdit(false);
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
  } = useForm<IUpdate>({
    resolver: zodResolver(updateSchema),
    defaultValues,
  });

  return (
    <Card.Root css={styles.card} variant="outline">
      <Card.Header>
        <Heading css={styles.heading}>Update your profile</Heading>
      </Card.Header>
      <Card.Body>
        <form onSubmit={handleSubmit(updateHandler)}>
          <VStack gap="4">
            <Field.Root invalid={!!errors.email} required>
              <Field.Label htmlFor="email">Email</Field.Label>
              <Input id="email" placeholder="email" {...register('email')} />
              <Field.ErrorText>{errors.email?.message}</Field.ErrorText>
            </Field.Root>

            <Button type="submit" w="200px" loading={isLoading}>
              Submit
            </Button>
          </VStack>
        </form>
      </Card.Body>
    </Card.Root>
  );
};

export default ProfileForm;
