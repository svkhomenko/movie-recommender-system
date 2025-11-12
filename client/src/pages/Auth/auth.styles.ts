import { type SystemStyleObject } from '@chakra-ui/react';

type TStyle = {
  card: SystemStyleObject;
  heading: SystemStyleObject;
  button: SystemStyleObject;
  footer: SystemStyleObject;
  footerText: SystemStyleObject;
  link: SystemStyleObject;
};

const styles: TStyle = {
  card: {
    width: '100%',
    p: { base: '10px 10px', md: '20px 30px' },
    maxW: '500px',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 10px 50px',
    backgroundColor: 'cardBg',
    border: 'none',
  },
  heading: {
    textAlign: 'center',
    color: 'accent.solid',
    fontSize: { base: '25px', sm: '30px' },
  },
  button: {
    w: '250px',
    colorPalette: 'accent',
  },
  footer: {
    marginTop: '25px',
  },
  footerText: {
    marginBottom: '10px',
  },
  link: {
    textDecoration: 'underline',
    color: 'accent.solid',
    _hover: {
      color: 'accent.hover',
    },
  },
};

export default styles;
