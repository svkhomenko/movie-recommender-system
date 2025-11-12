import { Button, Icon } from '@chakra-ui/react';
import useRequestHandler from '~/hooks/useRequestHandler';
import { useDeleteProfileMutation } from '~/store/api/profileSlice';
import { FiTrash2 } from 'react-icons/fi';
import AlertDialog from '~/components/AlertDialog';

const DeleteProfile = () => {
  const [deleteProfile, { isLoading: isDeleteLoading }] = useDeleteProfileMutation();

  const { handler: deleteHandler } = useRequestHandler<void>({
    f: deleteProfile,
    successMsg: 'Account was successfully deleted.',
  });

  const TriggerButtonProps = (
    <Button colorPalette="red" loading={isDeleteLoading}>
      Delete my account
      <Icon as={FiTrash2} />
    </Button>
  );

  const ConfirmButtonProps = (
    <Button onClick={() => deleteHandler()} colorPalette="red" loading={isDeleteLoading}>
      Delete my account
      <Icon as={FiTrash2} />
    </Button>
  );

  return (
    <AlertDialog
      TriggerButtonProps={TriggerButtonProps}
      title="Are you sure you want to delete your account?"
      ConfirmButtonProps={ConfirmButtonProps}
    />
  );
};

export default DeleteProfile;
