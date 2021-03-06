#include <StandardCplusplus.h>

// If this fails, install ArduinoSTL from the Arduino library
// and use the following instead:
// #include <ArduinoSTL.h>

#include <map>
#include <vector>
#include <algorithm> // std::find

// change it to \n in case of line termination is not \n\r
auto const terminator = '\r';
auto const separator = ' ';

std::map<String, String> parameters;

std::vector<String> random_measures;

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(50000);

  random_measures = { "mve", "vti", "vte" };
}

// this is tricky, didn't had the time to think a better algo
String parse_word(String const& command)
{
  auto const first_sep_pos = command.indexOf(separator);
  if (first_sep_pos == -1) {
    return command;
  }

  auto const second_sep_pos = command.indexOf(separator, first_sep_pos + 1);

  return command.substring(first_sep_pos + 1, second_sep_pos);
}

String set(String const& command)
{
  auto const name = parse_word(command);
  auto const value = parse_word(command.substring(name.length() + 4));
  parameters[name] = value;
  return "OK";
}

String get(String const& command)
{
  auto const name = parse_word(command);

  auto const it = std::find(
      random_measures.begin()
    , random_measures.end()
    , name
  );

  if (it != random_measures.end()) {
    return String(random(10, 40));
  } else {
    auto const it = parameters.find(name);

    return it == parameters.end() ? String("unknown") : it->second;
  }
}

void loop()
{
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil(terminator);
    command.trim();
    auto const command_type = command.substring(0, 3);

    if (command_type == "get") {
      Serial.println(get(command));
    } else if (command_type == "set") {
      Serial.println(set(command));
    } else {
      Serial.println("notok");
    }
  }
}

