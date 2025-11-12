import { type SystemStyleObject } from '@chakra-ui/react';

type TStyle = {
  card: SystemStyleObject;
};

const styles: TStyle = {
  card: {
    width: '100%',
    p: '10px 10px',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 10px 50px',
    backgroundColor: 'cardBg',
    border: 'none',
  },
};

export default styles;
