import { Alert, Box } from '@chakra-ui/react';
import Layout from '~/components/Layout';
import styles from './page-alert.styles';
import React from 'react';

type IProps = {
  status: 'info' | 'warning' | 'success' | 'error';
  title?: string | null;
  message: string;
  children?: React.ReactElement;
};

const PageAlert = ({ status, title = null, message, children }: IProps) => (
  <Layout>
    <Alert.Root status={status} css={styles.container}>
      <Alert.Indicator boxSize="40px" mr={0} />
      <Alert.Content>
        {title && (
          <Alert.Title mt={6} mr={0} fontSize="2xl">
            {title}
          </Alert.Title>
        )}
        <Alert.Description mt={5} maxWidth="sm" fontSize="md">
          {message}
        </Alert.Description>
        {children && <Box mt={7}>{children}</Box>}
      </Alert.Content>
    </Alert.Root>
  </Layout>
);

export default PageAlert;
