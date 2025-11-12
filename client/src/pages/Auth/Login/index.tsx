import { Box, Card, Heading, Link, Text } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import Layout from '~/components/Layout';
import styles from '../auth.styles';
import LoginForm from './LoginForm';

const Login = () => {
  return (
    <Layout>
      <Card.Root css={styles.card}>
        <Card.Header>
          <Heading css={styles.heading}>Log in to your account</Heading>
        </Card.Header>
        <Card.Body>
          <LoginForm />
          <Box css={styles.footer}>
            <Text css={styles.footerText}>
              Don't have an account yet?{' '}
              <Link asChild css={styles.link}>
                <ReactRouterLink to={'/register'}>Create one</ReactRouterLink>
              </Link>
            </Text>
          </Box>
        </Card.Body>
      </Card.Root>
    </Layout>
  );
};

export default Login;
