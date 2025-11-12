import { Heading, Link, Box, Card } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import SendPasswordConfirmationForm from './SendPasswordConfirmationForm';
import Layout from '~/components/Layout';
import styles from '../auth.styles';

const SendPasswordConfirmation = () => {
  return (
    <Layout>
      <Card.Root css={styles.card}>
        <Card.Header>
          <Heading css={styles.heading}>Send password confirmation</Heading>
        </Card.Header>
        <Card.Body>
          <SendPasswordConfirmationForm />
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

export default SendPasswordConfirmation;
