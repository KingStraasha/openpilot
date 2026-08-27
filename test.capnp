
@0x934efea7f017fff0;
struct ModelBundle { status @0 :Text; }
struct Msg {
    selectedBundle @0 :ModelBundle;
    availableBundles @1 :List(ModelBundle);
}
