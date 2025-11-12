import { Heading, Link, Box, Card } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import PasswordResetForm from './PasswordResetForm';
import Layout from '~/components/Layout';
import styles from '../auth.styles';

const PasswordReset = () => {
  return (
    <Layout>
      <Card.Root css={styles.card}>
        <Card.Header>
          <Heading css={styles.heading}>Reset password</Heading>
        </Card.Header>
        <Card.Body>
          <PasswordResetForm />
          <Box css={styles.footer}>
            <Link asChild css={styles.link}>
              <ReactRouterLink to={'/login'}>Go to the login page</ReactRouterLink>
            </Link>
          </Box>
        </Card.Body>
      </Card.Root>
    </Layout>
  );
};

export default PasswordReset;
