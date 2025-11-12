import { Box, Card, Heading, Link, Text } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import Layout from '~/components/Layout';
import styles from '../auth.styles';
import RegisterForm from './RegisterForm';

const Register = () => {
  return (
    <Layout>
      <Card.Root css={styles.card}>
        <Card.Header>
          <Heading css={styles.heading}>Create an account</Heading>
        </Card.Header>
        <Card.Body>
          <RegisterForm />
          <Box css={styles.footer}>
            <Text css={styles.footerText}>
              Already have an account?{' '}
              <Link asChild css={styles.link}>
                <ReactRouterLink to={'/login'}>Log in</ReactRouterLink>
              </Link>
            </Text>
          </Box>
        </Card.Body>
      </Card.Root>
    </Layout>
  );
};

export default Register;
