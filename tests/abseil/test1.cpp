#include <absl/container/flat_hash_set.h>

#include <iostream>
#include <string>

int main()
{
   absl::flat_hash_set<std::string> set2 = {{"huey"}, {"dewey"}, {"louie"},};

   for (auto& str: set2)
   {
      std::cout << str << "\n";
   }

   return 0;
}
