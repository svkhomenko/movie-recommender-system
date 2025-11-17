import { Flex, Heading } from '@chakra-ui/react';
type IProps = {
  message: string;
};

const NothingFound = ({ message }: IProps) => {
  return (
    <Flex minH="50px" alignItems="center" justifyContent="center" px="30px">
      <Heading fontWeight="medium">{message}</Heading>
    </Flex>
  );
};

export default NothingFound;
