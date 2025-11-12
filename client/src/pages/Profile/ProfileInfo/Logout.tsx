import { Button, Icon } from '@chakra-ui/react';
import useRequestHandler from '~/hooks/useRequestHandler';
import { useLogoutMutation } from '~/store/api/authSlice';
import { FiLogOut } from 'react-icons/fi';
import AlertDialog from '~/components/AlertDialog';

const Logout = () => {
  const [logout, { isLoading: isLogoutLoading }] = useLogoutMutation();

  const { handler: logoutHandler } = useRequestHandler<void>({
    f: logout,
  });

  const TriggerButtonProps = (
    <Button colorPalette="red" variant="outline" loading={isLogoutLoading}>
      Log out
      <Icon as={FiLogOut} />
    </Button>
  );

  const ConfirmButtonProps = (
    <Button onClick={() => logoutHandler()} colorPalette="red" loading={isLogoutLoading}>
      Log out
      <Icon as={FiLogOut} />
    </Button>
  );

  return (
    <AlertDialog
      TriggerButtonProps={TriggerButtonProps}
      title="Are you sure you want to log out?"
      ConfirmButtonProps={ConfirmButtonProps}
    />
  );
};

export default Logout;
