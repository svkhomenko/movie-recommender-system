import { type SystemStyleObject } from '@chakra-ui/react';

type StylesType = {
  card: SystemStyleObject;
  image: SystemStyleObject;
  heading: SystemStyleObject;
  icons: SystemStyleObject;
  text: SystemStyleObject;
};

const styles: StylesType = {
  card: {
    width: { base: '90%', md: '85%', xl: '100%' },
    margin: '0 auto',
    maxW: '1100px',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 10px 50px',
    display: 'flex',
    flexDirection: { base: 'column', md: 'row' },
    backgroundColor: 'cardBg',
    border: 'none',
    padding: '10px',
  },
  image: {
    maxW: { base: '100%', md: '300px' },
    w: { base: '100%', md: '300px' },
    h: 'auto',
    objectFit: 'contain',
    display: 'block',
    flexShrink: 0,
    flexGrow: 0,
    alignSelf: 'flex-start',
  },
  heading: {
    color: 'accent.solid',
    fontSize: { base: '25px', sm: '30px' },
  },
  icons: {
    mr: '-15px',
    gap: 1,
  },
  text: {
    '& span': {
      color: 'neutral.muted',
    },
  },
};

export default styles;
