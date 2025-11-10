import { Box, type BoxProps } from '@chakra-ui/react';
import styles from './container.styles';

const Container = ({ children, ...restProps }: BoxProps) => {
  return (
    <Box css={styles.container} h="100%" {...restProps}>
      {children}
    </Box>
  );
};

export default Container;
