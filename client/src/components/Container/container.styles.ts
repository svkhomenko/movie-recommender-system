import { type SystemStyleObject } from '@chakra-ui/react';

type TStyle = { container: SystemStyleObject };

const styles: TStyle = {
  container: {
    maxW: {
      base: '100%',
      md: '800px',
      lg: '1360px',
    },
    px: '15px',
    mx: 'auto',
  },
};

export default styles;
