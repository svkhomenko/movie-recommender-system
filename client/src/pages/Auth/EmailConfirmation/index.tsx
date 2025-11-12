import { useEffect } from 'react';
import { useSearchParams, Link as RouterLink } from 'react-router-dom';
import { Button } from '@chakra-ui/react';
import { useConfirmEmailMutation } from '~/store/api/authSlice';
import Loader from '~/components/Loader';
import PageAlert from '~/components/PageAlert';
import { type IError } from '~/types/error';

const AlertSuccess = () => {
  return (
    <PageAlert
      status="success"
      title="Email address confirmed"
      message="You have successfully confirm your email address. You can now login to the application."
    >
      <Button colorScheme="green" asChild>
        <RouterLink to="/login">Login</RouterLink>
      </Button>
    </PageAlert>
  );
};

const AlertError = ({ message }: { message: string }) => {
  return (
    <PageAlert status="error" title="Confirmation error!" message={message}>
      <Button colorScheme="red" asChild>
        <RouterLink to="/">Go home</RouterLink>
      </Button>
    </PageAlert>
  );
};

const EmailConfirmation = () => {
  const [searchParams] = useSearchParams();
  const confirmToken = searchParams.get('token');
  const [comfirmEmail, { isLoading, isError, error }] = useConfirmEmailMutation();

  useEffect(() => {
    if (confirmToken) {
      comfirmEmail({ confirmToken });
    }
  }, [confirmToken]);

  if (isLoading) {
    return <Loader />;
  }

  if (isError) {
    return <AlertError message={(error as IError).data.detail} />;
  }

  return <AlertSuccess />;
};

export default EmailConfirmation;
