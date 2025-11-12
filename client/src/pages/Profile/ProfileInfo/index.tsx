import { Button, Card, Flex, Icon, Heading, HStack, Stack, Wrap, StackSeparator } from '@chakra-ui/react';
import { FiEdit } from 'react-icons/fi';
import { Link } from 'react-router-dom';
import { useAppSelector } from '~/hooks/useAppSelector';
import Logout from './Logout';
import DeleteProfile from './DeleteProfile';
import styles from '../profile-card.styles';

type IProps = { setIsEdit: React.Dispatch<React.SetStateAction<boolean>> };

export const links = [
  { href: '/profile/ratings', label: 'Ratings' },
  { href: '/profile/watch-later', label: 'Watch Later' },
  { href: '/profile/watched', label: 'Watched' },
  { href: '/profile/viewing-history', label: 'Viewing History' },
];

const ProfileInfo = ({ setIsEdit }: IProps) => {
  const { user } = useAppSelector((state) => state.profile);

  return (
    <Card.Root css={styles.card} variant="outline">
      <Card.Header pb="1">
        <Flex flexDir="row" alignItems="center">
          <Heading size="lg" flexGrow="1">
            {user.email}
          </Heading>
          <Button onClick={() => setIsEdit(true)}>
            Edit
            <Icon as={FiEdit} />
          </Button>
        </Flex>
      </Card.Header>

      <Card.Body>
        <Stack separator={<StackSeparator />} gap="4">
          <HStack gap="4">
            {links.map((link) => (
              <Link key={link.href} to={link.href}>
                <Button variant="subtle">{link.label}</Button>
              </Link>
            ))}
          </HStack>
          <Wrap gap="4">
            <Link to="/password-reset">
              <Button variant="outline">Reset password</Button>
            </Link>
            <Logout />
            <DeleteProfile />
          </Wrap>
        </Stack>
      </Card.Body>
    </Card.Root>
  );
};

export default ProfileInfo;
