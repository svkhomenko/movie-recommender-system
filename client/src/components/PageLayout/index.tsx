import { Box } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import Header from '../Header';
import styles from './page-layout.styles';

const PageLayout = () => {
  return (
    <Box css={styles.main}>
      <Header />
      <Box>
        <Outlet />
      </Box>
    </Box>
  );
};

export default PageLayout;
