import { type SystemStyleObject } from '@chakra-ui/react';

type TStyle = { main: SystemStyleObject };

const styles: TStyle = {
  main: {
    position: 'relative',
    minHeight: '100vh',
    overflow: 'hidden',
    pt: '70px',
  },
};

export default styles;
