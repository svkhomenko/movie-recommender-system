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

type StylesTypeMediumCard = {
  card: SystemStyleObject;
  image: SystemStyleObject;
  heading: SystemStyleObject;
  text: SystemStyleObject;
  explanationBadge: SystemStyleObject;
};

export const stylesMediumCard: StylesTypeMediumCard = {
  card: {
    w: '100%',
    maxW: '300px',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 5px 20px',
    backgroundColor: 'cardBg',
    border: 'none',
    p: '10px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    gap: '2',
  },
  image: {
    w: '100%',
    maxW: '200px',
    h: 'auto',
    objectFit: 'cover',
    borderRadius: 'md',
  },
  heading: {
    color: 'accent.solid',
    fontSize: 'md',
    fontWeight: 'bold',
    lineClamp: 2,
  },
  text: {
    fontSize: 'sm',
    '& span': {
      color: 'neutral.muted',
    },
    lineClamp: 1,
  },
  explanationBadge: {
    position: 'absolute',
    top: '10px',
    left: '10px',
    zIndex: 10,
    padding: '4px 8px',
    fontSize: 'md',
    fontWeight: 'semibold',
    color: 'white',
    backgroundColor: 'accent.hover',
    opacity: 0.7,
    borderRadius: 'sm',
    backdropFilter: 'blur(3px)',
    textTransform: 'none',
  },
};

export default styles;
