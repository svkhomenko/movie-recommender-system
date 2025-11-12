import { Box, Button, ButtonGroup, HStack, Menu, Portal } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAppSelector } from '~/hooks/useAppSelector';
import useRequestHandler from '~/hooks/useRequestHandler';
import { useLogoutMutation } from '~/store/api/authSlice';

const NavbarAuth = () => {
  const navigate = useNavigate();
  const { user } = useAppSelector((state) => state.profile);

  const [logout] = useLogoutMutation();
  const { handler: logoutHandler } = useRequestHandler<void>({ f: logout });

  if (user.id) {
    return (
      <Box>
        <Menu.Root>
          <HStack gap={2}>
            <Menu.Trigger asChild>
              <Button variant="ghost" cursor="pointer">
                {user.email}
              </Button>
            </Menu.Trigger>
          </HStack>
          <Portal>
            <Menu.Positioner backgroundColor="pageBgShadow">
              <Menu.Content>
                <Menu.ItemGroup>
                  <Menu.ItemGroupLabel>Movies</Menu.ItemGroupLabel>
                  <Menu.Item value="Movies" px={4} py={2} onClick={() => navigate('/')}>
                    Movies
                  </Menu.Item>
                </Menu.ItemGroup>
                <Menu.Separator />
                <Menu.ItemGroup>
                  <Menu.ItemGroupLabel>Account</Menu.ItemGroupLabel>
                  <Menu.Item value="Settings" px={4} py={2} onClick={() => navigate('/profile')}>
                    Settings
                  </Menu.Item>
                  <Menu.Item value="Log out" px={4} py={2} color="red" onClick={() => logoutHandler()}>
                    Log out
                  </Menu.Item>
                </Menu.ItemGroup>
              </Menu.Content>
            </Menu.Positioner>
          </Portal>
        </Menu.Root>
      </Box>
    );
  }

  return (
    <ButtonGroup colorPalette="accent">
      <Button onClick={() => navigate('/login')}>Log in</Button>
      <Button variant="outline" onClick={() => navigate('/register')}>
        Sign up
      </Button>
    </ButtonGroup>
  );
};

export default NavbarAuth;
