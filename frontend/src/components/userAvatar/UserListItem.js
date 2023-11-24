import { Avatar } from "@chakra-ui/avatar";
import { Box, Text } from "@chakra-ui/layout";
import { ChatState } from "../../Context/ChatProvider";

const UserListItem = ({ handleFunction ,user}) => {
  // const { user } = ChatState();

  const urlS = process.env.REACT_APP_API_URL;
  console.log(user)
  const url = urlS.slice(0, -1);

  const imagesrc=url+user.pic

  return (
    <Box
      onClick={handleFunction}
      cursor="pointer"
      bg="#E8E8E8"
      _hover={{
        background: "#38B2AC",
        color: "white",
      }}
      w="100%"
      d="flex"
      alignItems="center"
      color="black"
      px={3}
      py={2}
      mb={2}
      borderRadius="lg"
    >
      <Avatar
        mr={2}
        size="sm"
        cursor="pointer"
        name={user.name}
        src={imagesrc}
      />
      <Box>
        <Text>{user.first_name}</Text>
        <Text fontSize="xs">
          <b>Username : </b>
          {user.username}
        </Text>
      </Box>
    </Box>
  );
};

export default UserListItem;
