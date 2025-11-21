import { type SystemStyleObject } from '@chakra-ui/react';

type StylesType = {
  card: SystemStyleObject;
  image: SystemStyleObject;
  infoOverlay: SystemStyleObject;
  heading: SystemStyleObject;
  text: SystemStyleObject;
  explanationBadge: SystemStyleObject;
};

export const styles: StylesType = {
  card: {
    w: '200px',
    maxW: '200px',
    boxShadow: 'rgba(19, 29, 54, 0.4) 0px 5px 20px',
    backgroundColor: 'cardBg',
    border: 'none',
    position: 'relative',
    overflow: 'hidden',
    _hover: {
      '& .info-overlay': {
        opacity: 1,
        transform: 'translateY(0)',
      },
    },
  },
  image: {
    w: '100%',
    h: '300px',
    objectFit: 'cover',
    display: 'block',
  },
  infoOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(19, 29, 54, 0.9)',
    backdropFilter: 'blur(5px)',
    color: 'white',
    padding: '10px',
    opacity: 0,
    transform: 'translateY(100%)',
    transition: 'opacity 0.3s ease-in-out, transform 0.3s ease-in-out',
    textAlign: 'left',
    display: 'flex',
    flexDirection: 'column',
    gap: '1',
    justifyContent: 'flex-end',
    height: '100%',
  },
  heading: {
    color: 'accent.solid',
    fontSize: 'md',
    fontWeight: 'bold',
    lineClamp: 2,
    textAlign: 'left',
  },
  text: {
    fontSize: 'xs',
    '& span': {
      color: 'neutral.muted',
    },
    textAlign: 'left',
  },
  explanationBadge: {
    position: 'absolute',
    top: '10px',
    left: '10px',
    zIndex: 10,
    padding: '4px 8px',
    fontSize: 'xs',
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
