import { Dialog, Button, Portal, CloseButton } from '@chakra-ui/react';
import styles from './alert-dialog.styles';

type IProps = {
  TriggerButtonProps: React.ReactElement;
  title: string;
  ConfirmButtonProps: React.ReactElement;
};

const AlertDialog = ({ TriggerButtonProps, title, ConfirmButtonProps }: IProps) => {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>{TriggerButtonProps}</Dialog.Trigger>
      <Portal>
        <Dialog.Backdrop />
        <Dialog.Positioner>
          <Dialog.Content css={styles.card}>
            <Dialog.Header>
              <Dialog.Title>{title}</Dialog.Title>
            </Dialog.Header>
            <Dialog.Footer>
              <Dialog.ActionTrigger asChild>
                <Button variant="outline">Cancel</Button>
              </Dialog.ActionTrigger>
              {ConfirmButtonProps}
            </Dialog.Footer>
            <Dialog.CloseTrigger asChild>
              <CloseButton size="sm" />
            </Dialog.CloseTrigger>
          </Dialog.Content>
        </Dialog.Positioner>
      </Portal>
    </Dialog.Root>
  );
};

export default AlertDialog;
