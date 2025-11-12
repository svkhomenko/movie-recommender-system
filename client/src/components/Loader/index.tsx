import { Spinner } from '@chakra-ui/react';
import Layout from '../Layout';

const Loader = ({ isFullScreen = true }) => {
  if (!isFullScreen) {
    return <Spinner size="lg" animationDuration=".6s" />;
  }

  return (
    <Layout>
      <Spinner
        css={{
          width: 100,
          height: 100,
        }}
        animationDuration=".6s"
        color="primaryText"
        borderWidth="4px"
      />
    </Layout>
  );
};

export default Loader;
