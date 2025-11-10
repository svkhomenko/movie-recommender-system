import { type SystemStyleObject } from '@chakra-ui/react';
import container from '../Container/container.styles';

type TStyle = { container: SystemStyleObject; navbar: SystemStyleObject };

const styles: TStyle = {
  navbar: {
    position: 'fixed',
    h: '70px',
    top: 0,
    right: 0,
    left: 0,
    bgColor: 'pageBg',
    zIndex: 100,
    py: '10px',
    transition: 'box-shadow 0.3s linear',
  },
  container: container.container,
};

export default styles;
