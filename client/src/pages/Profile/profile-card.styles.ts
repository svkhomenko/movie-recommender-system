import { type SystemStyleObject } from '@chakra-ui/react';

type StylesType = { card: SystemStyleObject; heading: SystemStyleObject };

const styles: StylesType = {
  card: {
    width: { base: '90%', md: '80%', xl: '65%' },
    margin: '0 auto',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 10px 50px',
    backgroundColor: 'cardBg',
    border: 'none',
  },
  heading: {
    textAlign: 'center',
    color: 'accent.solid',
    fontSize: { base: '25px', sm: '30px' },
  },
};

export default styles;
