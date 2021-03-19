// Create DB users

db.createUser({
  user: "kitchen",
  pwd: "5^2A5ubDwhk#&Xn&",
  roles: [
    {
      role: "readWrite",
      db: "cloudkitchensdb",
    },
  ],
});

db.createUser({
  user: "couriers",
  pwd: "u#Z6I8FPGHEq479n",
  roles: [
    {
      role: "readWrite",
      db: "cloudkitchensdb",
    },
  ],
});

db.createUser({
  user: "shelves",
  pwd: "HTBbK7z!N9kftjWK",
  roles: [
    {
      role: "readWrite",
      db: "cloudkitchensdb",
    },
  ],
});

db.createUser({
  user: "reporting",
  pwd: "Ic^s38cIy%L^mA83",
  roles: [
    {
      role: "readWrite",
      db: "cloudkitchensdb",
    },
  ],
});
